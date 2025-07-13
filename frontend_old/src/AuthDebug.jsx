import React from 'react';

export default function AuthDebug({ rawData }) {
  return (
    <div className="p-8 max-w-2xl mx-auto bg-white rounded shadow text-gray-800 mt-10">
      <h2 className="text-xl font-bold mb-4">🔍 No has iniciado sesión</h2>
      <p className="mb-2">
        El sistema no detecta sesión activa. Puedes hacer clic para iniciar sesión manualmente:
      </p>

      <div className="mb-4">
        <a
          href="/.auth/login/aad"
          className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700"
        >
          Iniciar sesión con Microsoft
        </a>
      </div>

      <h3 className="text-md font-semibold mb-2">📦 Respuesta de <code>/.auth/me</code>:</h3>
      <pre className="bg-gray-100 p-4 text-sm rounded overflow-auto">
        {rawData ? JSON.stringify(rawData, null, 2) : 'No se recibió respuesta.'}
      </pre>
    </div>
  );
}
