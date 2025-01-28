import React, { useEffect, useState } from 'react';
import { fetchTerms, createTerm, updateTerm, deleteTerm } from '../api';

export default function Admin() {
  const [terms, setTerms] = useState([]);
  const [form, setForm] = useState({ name: '', definition: '', source: '' });
  const [editId, setEditId] = useState(null);

  useEffect(() => {
    loadTerms();
  }, []);

  const loadTerms = async () => {
    const data = await fetchTerms();
    setTerms(data);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editId) {
      // update
      await updateTerm(editId, form);
    } else {
      // create
      await createTerm(form);
    }
    setForm({ name: '', definition: '', source: '' });
    setEditId(null);
    loadTerms();
  };

  const handleEdit = (term) => {
    setEditId(term.id);
    setForm({
      name: term.name,
      definition: term.definition,
      source: term.source || '',
    });
  };

  const handleDelete = async (id) => {
    await deleteTerm(id);
    loadTerms();
  };

  return (
    <div className="container">
      <h2>Админ</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '1rem' }}>
        <div>
          <label>Название: </label>
          <input 
            type="text" 
            name="name"
            value={form.name}
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Определение: </label>
          <textarea 
            name="definition"
            value={form.definition}
            onChange={handleChange} 
            rows={3}
            required
          />
        </div>
        <div>
          <label>Источник: </label>
          <input 
            type="text" 
            name="source"
            value={form.source}
            onChange={handleChange}
          />
        </div>
        <button type="submit">
          {editId ? 'Сохранить' : 'Создать'}
        </button>
        {editId && (
          <button type="button" onClick={() => {
            setEditId(null);
            setForm({ name: '', definition: '', source: '' });
          }}>
            Отмена
          </button>
        )}
      </form>

      <table border="1" cellPadding="4">
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Определение</th>
            <th>Источник</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {terms.map((term) => (
            <tr key={term.id}>
              <td>{term.id}</td>
              <td>{term.name}</td>
              <td>{term.definition}</td>
              <td>{term.source}</td>
              <td>
                <button onClick={() => handleEdit(term)}>Редактировать</button>
                <button onClick={() => handleDelete(term.id)}>Удалить</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
