import React from 'react';
import { FaPython, FaReact } from 'react-icons/fa';
import { SiTensorflow, SiNextdotjs, SiFlutter } from 'react-icons/si';
import './about.css';

const teamMembers = [
  {
    name: 'Namous Nassim',
    image: '/team/john.jpg',
    github: 'https://github.com/johndoe',
    linkedin: 'https://linkedin.com/in/johndoe',
  },
  {
    name: 'Fahd Benfaddoul',
    image: '/team/jane.jpg',
    github: 'https://github.com/janesmith',
    linkedin: 'https://linkedin.com/in/janesmith',
  },
  {
    name: 'Marouane Dbibih',
    image: '/team/jane.jpg',
    github: 'https://github.com/janesmith',
    linkedin: 'https://linkedin.com/in/janesmith',
  },
  
  {
    name: 'Achraf Eltouakki',
    image: '/team/jane.jpg',
    github: 'https://github.com/janesmith',
    linkedin: 'https://linkedin.com/in/janesmith',
  },
  {
    name: 'Ikram Souita',
    image: '/team/jane.jpg',
    github: 'https://github.com/janesmith',
    linkedin: 'https://linkedin.com/in/janesmith',
  },

  
  
];

const technologies = [
  { name: 'Python', logo: <FaPython className="technology-logo" />, description: 'Backend and OCR algorithms.' },
  { name: 'TensorFlow', logo: <SiTensorflow className="technology-logo" />, description: 'Advanced text recognition.' },
  { name: 'Next.js', logo: <SiNextdotjs className="technology-logo" />, description: 'Server-side rendering.' },
  { name: 'Flutter', logo: <SiFlutter className="technology-logo" />, description: 'Mobile application development.' },
  { name: 'React', logo: <FaReact className="technology-logo" />, description: 'Frontend web development.' },
];

export default function About() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-pink-100 flex items-center justify-center p-4 pt-20">
      <div className="w-full max-w-6xl bg-white rounded-2xl shadow-xl p-8 space-y-8">
        <div className="text-center">
          <div className="logo-icon mx-auto mb-4">⚡</div>
          <h2 className="text-4xl font-bold text-gray-800">About Our Project</h2>
          <p className="text-gray-500 mt-2">OCR Text Extraction from ID Cards</p>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-2xl font-semibold text-gray-800">Overview</h3>
            <p className="text-gray-600 mt-2">
              Our project leverages cutting-edge technologies to extract information from ID cards using Optical Character Recognition (OCR). We utilize Python and deep learning transformers to accurately recognize and extract text from images of ID cards.
            </p>
          </div>

          <div>
            <h3 className="text-2xl font-semibold text-gray-800">Technologies Used</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
              {technologies.map((tech) => (
                <div key={tech.name} className="technology-card">
                  {tech.logo}
                  <h4 className="text-lg font-semibold text-gray-800 mt-2">{tech.name}</h4>
                  <p className="text-gray-600 text-sm">{tech.description}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
  <h3 className="text-2xl font-semibold text-gray-800 border-b-2 border-gray-300 pb-2 mb-4">
    Features
  </h3>
  <ul className="list-disc list-inside text-gray-700 space-y-2">
    <li>
      <span className="text-gray-900 font-medium">Accurate text extraction:</span> Supports various types of ID cards with high precision.
    </li>
    <li>
      <span className="text-gray-900 font-medium">Real-time processing:</span> Validate and process extracted information instantly.
    </li>
    <li>
      <span className="text-gray-900 font-medium">User-friendly interfaces:</span> Designed for seamless interaction on both web and mobile platforms.
    </li>
    <li>
      <span className="text-gray-900 font-medium">Secure handling:</span> Protect sensitive information with advanced encryption and data protection.
    </li>
  </ul>
</div>

          <div>
            <h3 className="text-2xl font-semibold text-gray-800">Team</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-4">
              {teamMembers.map((member) => (
                <div key={member.name} className="team-member text-center">
                  <img
                    src={member.image}
                    alt={member.name}
                    className="w-24 h-24 mx-auto"
                  />
                  <h4 className="text-lg font-semibold text-gray-800 mt-2">{member.name}</h4>
                  <div className="social-links flex justify-center mt-2">
                    <a href={member.github} target="_blank" rel="noopener noreferrer">
                      <i className="fab fa-github"></i>
                    </a>
                    <a href={member.linkedin} target="_blank" rel="noopener noreferrer">
                      <i className="fab fa-linkedin"></i>
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

        
        </div>
      </div>
    </div>
  );
}
