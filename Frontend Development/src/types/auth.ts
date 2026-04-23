export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}
