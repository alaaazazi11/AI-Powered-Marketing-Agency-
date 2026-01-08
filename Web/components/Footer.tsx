
import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-100 py-12 mt-20">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-2xl font-bold text-indigo-600 mb-4">E3lanak</p>
        <p className="text-gray-500 max-w-md mx-auto mb-8">
          Revolutionizing marketing with AI. Create professional ads in seconds, not hours.
        </p>
        <div className="text-sm text-gray-400">
          © {new Date().getFullYear()} E3lanak AI Marketing Platform. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
