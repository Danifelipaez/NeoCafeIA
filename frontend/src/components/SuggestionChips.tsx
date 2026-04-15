'use client';

import React from 'react';

interface SuggestionChipsProps {
  suggestions: string[];
  onSelect: (suggestion: string) => void;
}

export function SuggestionChips({ suggestions, onSelect }: SuggestionChipsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          onClick={() => onSelect(suggestion)}
          className="px-3 py-2 bg-accent-light text-dark text-sm font-medium rounded-full hover:bg-accent transition-colors duration-300"
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
}
