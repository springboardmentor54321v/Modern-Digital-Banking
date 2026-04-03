function base64UrlDecode(input) {
  const base64 = input.replace(/-/g, "+").replace(/_/g, "/");
  const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), "=");
  const decoded = atob(padded);
  try {
    return decodeURIComponent(
      decoded
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
  } catch {
    return decoded;
  }
}

export function getUserIdFromAuth() {
  const token = localStorage.getItem("access_token");
  if (token) {
    const parts = token.split(".");
    if (parts.length === 3) {
      try {
        const payload = JSON.parse(base64UrlDecode(parts[1]));
        const userId = payload?.user_id ?? payload?.id;
        if (typeof userId === "number") return userId;
        if (typeof userId === "string" && userId.trim()) return Number(userId);
      } catch {
        // ignore
      }
    }
  }

  const userStr = localStorage.getItem("user");
  if (!userStr) return null;
  try {
    const user = JSON.parse(userStr);
    return user?.id ?? null;
  } catch {
    return null;
  }
}

