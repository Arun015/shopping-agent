import React from 'react';

const SuggestedQueries = ({ onQueryClick }) => {
  const queries = [
    "Best camera phone under ₹30,000?",
    "Compare Pixel 8a vs OnePlus 12R",
    "Show me Samsung phones under ₹25k",
    "Battery king with fast charging around ₹15k",
    "Explain OIS vs EIS",
    "Compact Android phone for one-hand use"
  ];

  return (
    <div className="mb-6">
      <p className="text-sm text-gray-600 mb-3">Try asking:</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {queries.map((query, index) => (
          <button
            key={index}
            onClick={() => onQueryClick(query)}
            className="text-left px-4 py-2 bg-white border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors text-sm"
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  );
};

export default SuggestedQueries;



