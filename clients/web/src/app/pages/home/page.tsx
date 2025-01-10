import './home.css'
export default function HomePage() {
    return (
      <div className="bg-gray-50 min-h-screen">
        
        <div className="relative pt-20 pb-32 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center">
          <h1 className="text-4xl font-extrabold mb-4">Welcome to Our Service</h1>
          <p className="text-lg mb-8">
            We offer cutting-edge solutions to make your life easier.
          </p>
          <div className="flex justify-center space-x-6">
            <button className="bg-white text-blue-700 py-3 px-6 rounded-lg shadow-lg hover:bg-blue-100 transition duration-300">
              Learn More
            </button>
            <button className="bg-transparent border-2 border-white text-white py-3 px-6 rounded-lg hover:bg-white hover:text-blue-700 transition duration-300">
              Get Started
            </button>
          </div>
        </div>
  
       
        <div className="py-16 px-4 sm:px-8 bg-white">
          <h2 className="text-3xl font-bold text-gray-800 text-center mb-8">
            Why Choose Us?
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">

            <div className="bg-gray-100 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Feature One</h3>
              <p className="text-gray-600">
                Benefit from our top-quality feature that provides outstanding results.
              </p>
            </div>
  
            
            <div className="bg-gray-100 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Feature Two</h3>
              <p className="text-gray-600">
                Enjoy a user-friendly experience with seamless integration and accessibility.
              </p>
            </div>
  
           
            <div className="bg-gray-100 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Feature Three</h3>
              <p className="text-gray-600">
                Our solutions ensure maximum performance with security at its core.
              </p>
            </div>
          </div>
        </div>
  
      
        <div className="py-16 px-4 sm:px-8 bg-blue-600 text-white text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-lg mb-8">Join us today and take the first step towards excellence.</p>
          <button className="bg-white text-blue-600 py-3 px-6 rounded-lg shadow-lg hover:bg-blue-100 transition duration-300">
            Start Now
          </button>
        </div>
      </div>
    );
  }
  