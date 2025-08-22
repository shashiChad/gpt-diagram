import React from 'react'

export default function SubmissionsList({submissions = [], deleteSubmission}){
  return (
    <section className="saved">
      <div className="saved-header">
        <h2 className="saved-title">Saved Message</h2>
        <span className="saved-count">{submissions.length} total</span>
      </div>

      {submissions.length === 0 ? (
        <p className="saved-empty">please submit the form!!</p>
      ) : (
        <ul className="saved-list">
          {submissions.map((s) => (
            <li key={s.id} className="saved-item">
              <p className="saved-text">{s.message}</p>
              <div className="saved-actions">
                <button className="saved-delete" onClick={() => deleteSubmission(s.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>

  );
}


  


