import React from 'react';

export default function LogoPlaceholder() {
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 16}}>
      <img src="/assets/png/logo-minimal-128.png" alt="Coder logo" width={128} height={128} />
      <div>
        <h1>Coder</h1>
        <p>AI-проект для анализа, исправления и улучшения кода.</p>
      </div>
    </div>
  );
}
