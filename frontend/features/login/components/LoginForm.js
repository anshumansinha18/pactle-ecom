"use client";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { LOGIN_FIELDS, LOGIN_FIELD_CONFIG } from "../constants";
import { loginValidationSchema } from "../utils/validation";
import { handleLoginSubmit } from "../utils";
import { renderField } from "../utils/fieldtocomponentmapper";
import React from "react";

export default function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    resolver: yupResolver(loginValidationSchema),
    defaultValues: {
      [LOGIN_FIELDS.USERNAME]: "",
      [LOGIN_FIELDS.PASSWORD]: "",
    },
  });

  const onSubmit = (data) => {
    handleLoginSubmit(data);
    reset(); // Reset form after successful submission
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            {Object.values(LOGIN_FIELDS).map((field) => (
              <React.Fragment key={field}>
                {renderField(
                  field,
                  LOGIN_FIELD_CONFIG[field],
                  register,
                  errors[field]
                )}
              </React.Fragment>
            ))}
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
