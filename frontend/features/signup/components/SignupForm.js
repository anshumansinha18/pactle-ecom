"use client";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { SIGNUP_FIELDS, SIGNUP_FIELD_CONFIG } from "../constants";
import { signupValidationSchema } from "../utils/validation";
import { handleSignupSubmit } from "../utils";
import { renderField } from "../utils/fieldtocomponentmapper";
import React from "react";

export default function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    resolver: yupResolver(signupValidationSchema),
    defaultValues: {
      [SIGNUP_FIELDS.USERNAME]: "",
      [SIGNUP_FIELDS.EMAIL]: "",
      [SIGNUP_FIELDS.PASSWORD]: "",
      [SIGNUP_FIELDS.CONFIRM_PASSWORD]: "",
    },
  });

  const onSubmit = (data) => {
    handleSignupSubmit(data);
    reset(); // Reset form after successful submission
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign up for an account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            {Object.values(SIGNUP_FIELDS).map((field) => (
              <React.Fragment key={field}>
                {renderField(
                  field,
                  SIGNUP_FIELD_CONFIG[field],
                  register,
                  errors[field]
                )}
              </React.Fragment>
            ))}
          </div>

          <div>
            <button
              type="submit"
              className="relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
