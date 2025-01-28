const API_URL = 'http://localhost:8080'; 
// Если запускаете через docker-compose, возможно понадобится 'http://backend:8080' 
// или прописать прокси в package.json.


// ============ Термины ============

// Получить все термины
export async function fetchTerms() {
  const response = await fetch(`${API_URL}/terms`);
  return response.json();
}

// Создать новый термин
export async function createTerm(termData) {
  const response = await fetch(`${API_URL}/terms`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(termData),
  });
  return response.json();
}

// Редактировать термин
export async function updateTerm(termId, updates) {
  const response = await fetch(`${API_URL}/terms/${termId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates),
  });
  return response.json();
}

// Удалить термин
export async function deleteTerm(termId) {
  const response = await fetch(`${API_URL}/terms/${termId}`, {
    method: 'DELETE',
  });
  return response.json();
}


// ============ Связи ============

// Получить все связи
export async function fetchRelationships() {
  const response = await fetch(`${API_URL}/relationships`);
  return response.json();
}

// Создать новую связь
export async function createRelationship(relData) {
  const response = await fetch(`${API_URL}/relationships`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(relData),
  });
  return response.json();
}

// Обновить связь
export async function updateRelationship(relationshipId, relData) {
  const response = await fetch(`${API_URL}/relationships/${relationshipId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(relData),
  });
  return response.json();
}

// Удалить связь
export async function deleteRelationship(relationshipId) {
  const response = await fetch(`${API_URL}/relationships/${relationshipId}`, {
    method: 'DELETE',
  });
  return response.json();
}
