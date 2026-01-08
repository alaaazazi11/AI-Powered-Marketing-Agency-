
import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Image as ImageIcon, MessageSquare, Zap } from 'lucide-react';

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="animate-fade-in-up">
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-6">
              Your Marketing <span className="text-indigo-600">On Autopilot</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
              Describe your product and let our AI generate complete, high-converting social media ads including stunning visuals and persuasive copy.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link 
                to="/create" 
                className="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 md:text-xl transition-all shadow-lg hover:shadow-indigo-500/25"
              >
                Create Your Ad Now
                <Zap className="ml-2 w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose E3lanak?</h2>
            <p className="text-gray-600">Powerful features to scale your brand faster than ever.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<ImageIcon className="text-indigo-600 w-8 h-8" />}
              title="AI Image Generation"
              description="High-resolution, studio-quality product photos tailored to your description."
            />
            <FeatureCard 
              icon={<MessageSquare className="text-indigo-600 w-8 h-8" />}
              title="Copywriting Assistant"
              description="Persuasive ad copy designed to maximize conversions on any platform."
            />
            <FeatureCard 
              icon={<Sparkles className="text-indigo-600 w-8 h-8" />}
              title="Brand Consistency"
              description="Maintain a professional look across all your social media channels."
            />
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="bg-indigo-600 py-20 text-center">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-extrabold text-white mb-8">Ready to transform your marketing?</h2>
          <Link to="/create" className="inline-block bg-white text-indigo-600 px-10 py-4 rounded-xl font-bold text-xl hover:bg-gray-100 transition-colors shadow-lg">
            Get Started for Free
          </Link>
        </div>
      </section>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) => (
  <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
    <div className="mb-6">{icon}</div>
    <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
  </div>
);

export default LandingPage;
