export const SIGNUP_FIELDS = {
  USERNAME: "username",
  EMAIL: "email",
  PASSWORD: "password",
  CONFIRM_PASSWORD: "confirmPassword",
};

export const SIGNUP_FIELD_CONFIG = {
  [SIGNUP_FIELDS.USERNAME]: {
    label: "Username",
    placeholder: "Enter your username",
    type: "text",
  },
  [SIGNUP_FIELDS.EMAIL]: {
    label: "Email",
    placeholder: "Enter your email",
    type: "email",
  },
  [SIGNUP_FIELDS.PASSWORD]: {
    label: "Password",
    placeholder: "Enter your password",
    type: "password",
  },
  [SIGNUP_FIELDS.CONFIRM_PASSWORD]: {
    label: "Confirm Password",
    placeholder: "Confirm your password",
    type: "password",
  },
};
