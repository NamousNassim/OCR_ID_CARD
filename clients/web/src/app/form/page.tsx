"use client";
import React, { useState } from "react";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<any | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleFormSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!file) {
      alert("Please upload a file before submitting.");
      return;
    }

    setIsLoading(true);

    try {
      // Prepare the file for upload
      const formData = new FormData();
      formData.append("document", file);

      // Send the file to Mindee API
      const response = await fetch("https://api.mindee.net/v1/products/mindee/international_id/v2/predict_async", {
        method: "POST",
        headers: {
          "Authorization": `Token f022cfdc9ba73c5165d866f1907ea8e5`,
        },
        body: formData,
      });

      const data = await response.json();
      console.log("POST response:", data);
      const jobId = data.job.id;

      // Polling function to check job status
      const checkJobStatus = async () => {
        const statusResponse = await fetch(`https://api.mindee.net/v1/products/mindee/international_id/v2/documents/queue/${jobId}`, {
          method: "GET",
          headers: {
            "Authorization": `Token f022cfdc9ba73c5165d866f1907ea8e5`,
          },
        });

        const statusData = await statusResponse.json();
        console.log("GET response:", statusData);

        if (statusData.job.status === "completed") {
          setApiResponse(statusData);
          setIsLoading(false);
        } else {
          setTimeout(checkJobStatus, 5000); // Retry after 5 seconds
        }
      };

      checkJobStatus();
    } catch (error) {
      console.error("Error uploading the file:", error);
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center mb-4">Upload an ID</h1>
        <form onSubmit={handleFormSubmit}>
          <input
            type="file"
            accept="image/*,application/pdf"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          />
          <button
            type="submit"
            disabled={isLoading}
            className={`mt-4 w-full px-4 py-2 text-white font-bold rounded-lg ${
              isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"
            }`}
          >
            {isLoading ? "Uploading..." : "Submit"}
          </button>
        </form>

        {/* Show API response */}
        {apiResponse && apiResponse.document && apiResponse.document.inference && (
          <div className="mt-6 bg-gray-50 p-4 rounded-md shadow-md">
            <h2 className="text-xl font-semibold mb-2">Response</h2>
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Country</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.country_of_issue.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Document Type</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.document_type.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Last Name</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.surnames.map((surname: any) => surname.value).join(", ") || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">First Name</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.given_names.map((name: any) => name.value).join(", ") || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Birth Date</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.birth_date.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Birth Place</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.birth_place.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">ID Number</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.document_number.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">CAN Number</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.personal_number.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Expiry Date</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.expiry_date.value || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Additional Info</label>
                <input
                  type="text"
                  value={apiResponse.document.inference.prediction.additional_info || ""}
                  readOnly
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;