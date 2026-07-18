from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Document, DocEmbedding
from app import db
import json

bp = Blueprint('ai', __name__)


def _cosine(a, b):
    # a and b are lists of floats
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _get_embedding(text):
    key = current_app.config.get('OPENAI_API_KEY')
    if not key:
        return None
    try:
        import openai
        openai.api_key = key
        resp = openai.Embedding.create(model='text-embedding-3-small', input=text)
        emb = resp['data'][0]['embedding']
        return emb
    except Exception:
        return None


@bp.route('/ingest', methods=['POST'])
@jwt_required()
def ingest():
    """Ingest a document, compute embedding (if available), and store."""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    title = data.get('title')
    content = data.get('content')
    source_url = data.get('source_url')
    if not content:
        return jsonify({'msg': 'content required'}), 400
    doc = Document(user_id=user_id, title=title, content=content, source_url=source_url)
    db.session.add(doc)
    db.session.commit()

    emb = _get_embedding(content)
    if emb is not None:
        db_emb = DocEmbedding(document_id=doc.id, embedding=json.dumps(emb))
        db.session.add(db_emb)
        db.session.commit()

    return jsonify({'id': doc.id}), 201


@bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    data = request.get_json() or {}
    query = data.get('query')
    top_k = int(data.get('top_k', 4))
    if not query:
        return jsonify({'msg': 'query required'}), 400
    q_emb = _get_embedding(query)
    if q_emb is None:
        return jsonify({'msg': 'embeddings not available (OPENAI_API_KEY missing)'}), 400

    # fetch embeddings for documents visible to user
    user_id = get_jwt_identity()
    rows = db.session.query(DocEmbedding, Document).join(Document, DocEmbedding.document_id == Document.id).filter((Document.user_id == user_id) | (Document.user_id == None)).all()
    scored = []
    for emb_row, doc in rows:
        try:
            doc_emb = json.loads(emb_row.embedding)
            score = _cosine(q_emb, doc_emb)
            scored.append((score, doc))
        except Exception:
            continue
    scored.sort(key=lambda x: x[0], reverse=True)
    out = []
    for score, doc in scored[:top_k]:
        out.append({'id': doc.id, 'title': doc.title, 'source_url': doc.source_url, 'score': score, 'content_snippet': (doc.content[:500] + '...') if doc.content else ''})
    return jsonify({'results': out})


@bp.route('/ask', methods=['POST'])
@jwt_required()
def ask():
    data = request.get_json() or {}
    query = data.get('query')
    if not query:
        return jsonify({'msg': 'query required'}), 400

    # perform search if embeddings available
    q_emb = _get_embedding(query)
    sources_out = []
    if q_emb is not None:
        # reuse search logic
        rows = db.session.query(DocEmbedding, Document).join(Document, DocEmbedding.document_id == Document.id).filter((Document.user_id == get_jwt_identity()) | (Document.user_id == None)).all()
        scored = []
        for emb_row, doc in rows:
            try:
                doc_emb = json.loads(emb_row.embedding)
                score = _cosine(q_emb, doc_emb)
                scored.append((score, doc))
            except Exception:
                continue
        scored.sort(key=lambda x: x[0], reverse=True)
        for score, doc in scored[:4]:
            sources_out.append({'id': doc.id, 'title': doc.title, 'source_url': doc.source_url, 'score': score, 'content_snippet': (doc.content[:500] + '...') if doc.content else ''})

    # Build prompt and call OpenAI (ChatCompletion) if key present
    answer = None
    key = current_app.config.get('OPENAI_API_KEY')
    if key:
        try:
            import openai
            openai.api_key = key
            system = "You are an assistant that helps users prioritize and plan tasks based on user documents. Provide concise steps and cite sources."
            context_text = ''
            for s in sources_out:
                context_text += f"Source: {s.get('title') or 'untitled'}\n{ s.get('content_snippet') }\nURL: { s.get('source_url') or '' }\n---\n"
            user_msg = f"Context:\n{context_text}\nQuestion: {query}\nPlease provide a short prioritized plan and list sources used."
            resp = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': user_msg}], max_tokens=400)
            answer = resp.choices[0].message.content.strip()
        except Exception as e:
            answer = f"OpenAI call failed: {str(e)}"
    else:
        # fallback: simple heuristic answer
        answer = f"(stub) Prioritized suggestions for: {query}"

    return jsonify({'answer': answer, 'sources': sources_out})
