export default function SignedOut() {
  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold mb-4">Sesión cerrada</h1>
      <p>
        Puedes <a href="/.auth/login/aad" className="text-blue-600 underline">iniciar sesión</a> de nuevo.
      </p>
    </div>
  );
}
