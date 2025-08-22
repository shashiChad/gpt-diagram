import { useState } from 'react'
import UserForm from './components/UserForm'
import SubmissionsList from './components/SubmissionsList';
import useLocalStorage from './hooks/useLocalStorage';
import './App.css';
import logo from './assets/logo.webp';



export default function App(){
    const [form, setForm] = useState({
      message:"",
    });
    const [submissions, setSubmissions] = useLocalStorage([]);
    const [savedToast, setsavedToast] = useState(false)

    const handleChange = (e) => setForm({...form,[e.target.name]: e.target.value})
    const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.message.trim()) return alert('Message is required')
    setSubmissions([{ ...form, id: Date.now() }, ...submissions])
    clearForm()
    setSavedToast(true)
    setTimeout(() => setSavedToast(false), 1500)
  }
  const clearForm = () => setForm({ message: '' })
  const clearAll = () => setSubmissions([])
  const deleteSubmission = (id) => setSubmissions(submissions.filter(s => s.id !== id));
   return (
    
<div className="min-h-screen bg-slate-50 flex items-start justify-center py-12 px-4">
<div className="min-h-screen bg-slate-50 flex items-start justify-center py-12 px-4">
  <div className="flex justify-center items-center mb-6">
    <img src={logo} alt="Logo" className="h-16 w-16 rounded-full shadow-md" />
    <h1 className="ml-3 text-2xl font-bold text-gray-700">Simple User Form</h1>
  </div>

  <div className="container">
    <h2 className="text-2xl font-semibold mb-4">Simple User Form</h2>

    <div className="form-section flex gap-6">
      <div className="w-1/2">
        <UserForm
          form={form}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
          clearAll={clearAll}
          clearForm={clearForm}
        />
        {savedToast && (
          <div className="mt-4 text-sm text-green-700">
            Saved — refresh and you'll still see it.
          </div>
        )}
        <hr className="my-6" />
      </div>

      <div className="saved-section w-1/2">
        <SubmissionsList submissions={submissions} deleteSubmission={deleteSubmission} />
      </div>
    </div>
  </div>
</div>
</div>
/* <h1 className="text-2xl font-semibold mb-4">Simple User Form</h1>
<div className="flex gap-6">
<div className="w-1/2">
<UserForm 
form={form} 
handleChange={handleChange} 
handleSubmit={handleSubmit} 
clearAll={clearAll} 
clearForm={clearForm}/>
        {savedToast && <div className="mt-4 text-sm text-green-700">Saved — refresh and you'll still see it.</div>}
                <hr className="my-6" />
                </div>
<div className="w-1/2">
<SubmissionsList 
submissions={submissions} deleteSubmission={deleteSubmission}/>
</div>
</div>
      </div> */
    
  )
}


  


