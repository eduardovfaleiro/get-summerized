export async function safeRequest(request) {
  try {
    return await request();
  } catch (error) {
    return null;
  }
}
