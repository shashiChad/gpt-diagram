import React from 'react'

export default function UserForm({ form, handleChange, handleSubmit, clearAll, clearForm }) {
  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h2>Simple User Form</h2>

      <textarea
        name="message"
        value={form.message}
        onChange={handleChange}
        placeholder="write here....."
      ></textarea>

      <div className="buttons">
        <button type="submit" className="btn-submit">Submit</button>
        <button type="button" onClick={clearForm} className="btn-reset">Reset</button>
        <button type="button" onClick={clearAll} className="btn-clear">Clear All</button>
      </div>
    </form>
  );
}

  

