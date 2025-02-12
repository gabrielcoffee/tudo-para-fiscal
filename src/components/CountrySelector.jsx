"use client"

import { useState, useRef, useEffect } from "react"
import { Check, ChevronDown } from "lucide-react"

export default function CountrySelector({selectedCountry, setSelectedCountry}) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  // Close dropdown if the user clicks outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        className="w-[120px] justify-between px-4 py-2 border border-gray-300 rounded-md flex items-center"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selectedCountry}
        <ChevronDown className="ml-2 h-4 w-4" />
      </button>

      {isOpen && (
        <div className="absolute mt-1 w-[120px] bg-white border border-gray-300 rounded-lg shadow-lg z-10">
          <div
            className="px-4 py-2 cursor-pointer hover:bg-gray-100 flex justify-between"
            onClick={() => {
              setSelectedCountry("Brasil")
              setIsOpen(false)
            }}
          >
            Brasil {selectedCountry === "Brasil" && <Check className="ml-auto h-4 w-4" />}
          </div>
          <div
            className="px-4 py-2 cursor-pointer hover:bg-gray-100 flex justify-between"
            onClick={() => {
              setSelectedCountry("EUA")
              setIsOpen(false)
            }}
          >
            EUA {selectedCountry === "EUA" && <Check className="ml-auto h-4 w-4" />}
          </div>
        </div>
      )}
    </div>
  )
}
