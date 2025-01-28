import React, { useEffect, useRef, useState } from 'react';
import { fetchTerms, fetchRelationships } from '../api';
import { Network } from 'vis-network/standalone';
import '../App.css';

export default function Graph() {
  const networkRef = useRef(null);
  const [terms, setTerms] = useState([]);
  const [relationships, setRelationships] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (terms.length > 0 && relationships.length > 0) {
      buildNetwork();
    }
  }, [terms, relationships]);

  const loadData = async () => {
    const t = await fetchTerms();
    const r = await fetchRelationships();
    setTerms(t);
    setRelationships(r);
  };

  const buildNetwork = () => {
    const nodes = terms.map((term) => ({
      id: term.id,
      label: term.name,
    }));

    const edges = relationships.map((rel) => ({
      from: rel.source_term_id,
      to: rel.target_term_id,
      label: rel.relation_type || '',
      arrows: 'to',
    }));

    const container = networkRef.current;
    const data = { nodes, edges };
    const options = {
      nodes: {
        shape: 'box',
        color: {
          background: '#ffffff',
          border: '#ff90af',
        },
        font: { color: '#000' },
      },
      edges: {
        color: '#ff90af',
        font: { align: 'horizontal' },
        smooth: { type: 'cubicBezier' },
      },
      physics: {
        enabled: true,
        stabilization: { iterations: 500 }
      },
      layout: {
        improvedLayout: true
      }
    };

    new Network(container, data, options);
  };

  return (
    <div className="container">
      <h2>Семантический граф</h2>
      <div 
        ref={networkRef} 
        style={{ height: '600px', border: '1px solid #ccc', borderRadius: '8px' }}
      />
    </div>
  );
}
