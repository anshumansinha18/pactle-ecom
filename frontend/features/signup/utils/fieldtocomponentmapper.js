import React from "react";

// Base input component for react-hook-form
const BaseInput = ({ field, config, register, error }) => {
  // Get the register object for this field
  const registerField = register(field);

  return (
    <div>
      <label htmlFor={field} className="sr-only">
        {config.label}
      </label>
      <input
        id={field}
        name={field}
        type={config.type}
        onChange={registerField.onChange}
        onBlur={registerField.onBlur}
        ref={registerField.ref}
        className="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
        placeholder={config.placeholder}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error.message}</p>}
    </div>
  );
};

// Field type to component mapping
export const FIELD_TYPE_MAPPER = {
  text: BaseInput,
  email: BaseInput,
  password: BaseInput,
};

// Helper function to render field based on type with react-hook-form
export const renderField = (field, config, register, error) => {
  const Component = FIELD_TYPE_MAPPER[config.type] || FIELD_TYPE_MAPPER.text;
  return (
    <Component
      key={field}
      field={field}
      config={config}
      register={register}
      error={error}
    />
  );
};
