export default async function sendMessage(message) {
  return new Promise((resolve) =>
    setTimeout(
      () =>
        resolve({
          response: `Mock response: "${message}" received. Backend not connected yet.`
        }),
      500
    )
  );
}
