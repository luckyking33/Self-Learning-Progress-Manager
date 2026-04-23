import client from "@/api/client";
import type { ApiEnvelope, MockUser } from "@/types/course";
import type { AuthToken, RegisterPayload } from "@/types/auth";

export async function register(payload: RegisterPayload): Promise<AuthToken> {
  const response = await client.post<ApiEnvelope<AuthToken>>("/auth/register", payload);
  return response.data.data;
}

export async function login(identity: string, password: string): Promise<AuthToken> {
  const body = new URLSearchParams();
  body.set("username", identity);
  body.set("password", password);

  const response = await client.post<ApiEnvelope<AuthToken>>("/auth/login", body, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  return response.data.data;
}

export async function fetchMe(): Promise<MockUser> {
  const response = await client.get<ApiEnvelope<MockUser>>("/users/me");
  return response.data.data;
}
