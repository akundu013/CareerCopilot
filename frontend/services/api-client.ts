import { auth } from "@/services/firebase";

interface ApiRequestOptions extends RequestInit {
  authRequired?: boolean;
}

export interface ApiUser {
  uid: string;
  email: string | null;
  email_verified: boolean | null;
}

function getApiUrl() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!apiUrl) {
    throw new Error("Missing NEXT_PUBLIC_API_URL environment variable.");
  }

  return apiUrl.replace(/\/$/, "");
}

async function getAuthorizationHeader() {
  const user = auth.currentUser;

  if (!user) {
    throw new Error("You must be logged in to call this endpoint.");
  }

  const token = await user.getIdToken();

  return `Bearer ${token}`;
}

export async function apiRequest<TResponse>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<TResponse> {
  const { authRequired = true, headers, ...requestOptions } = options;
  const requestHeaders = new Headers(headers);

  if (authRequired) {
    requestHeaders.set("Authorization", await getAuthorizationHeader());
  }

  const response = await fetch(`${getApiUrl()}${path}`, {
    ...requestOptions,
    headers: requestHeaders,
  });

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}.`);
  }

  if (response.status === 204) {
    return undefined as TResponse;
  }

  return response.json() as Promise<TResponse>;
}

export function getCurrentUserFromApi() {
  return apiRequest<ApiUser>("/api/auth/me");
}
