import React from 'react'

export default function GenerateButton({onGenerate}) {
  return (
    <button
    onClick={onGenerate}
    className="px-4 py-2 bg-blue-600 rounded-md hover:bg-blue-500 transition text-sm font-medium w-fit self-start"
    >
     Generate 
    </button>
  )
}

