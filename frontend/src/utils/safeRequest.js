export async function safeRequest(request) {
  try {
    return await request();
  } catch (error) {
    // erro já foi tratado no interceptor
    return null;
  }
}
