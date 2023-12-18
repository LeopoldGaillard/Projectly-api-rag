import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const [dataType, setDataType] = useState("No data type provided");
  const DATA_TYPES = [
    "Hourly Cost",
    "Bill",
    "Contract",
    "Order Form",
    "Bank Balance",
    "Other",
  ];

  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    setMessage("");
    setIsError(false);

    const formData = new FormData();

    formData.append("file", file);
    formData.append("description", description);
    formData.append("dataType", dataType);

    try {
      await axios.post(
        "http://127.0.0.1:5000/projectly/docs/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setMessage("File uploaded successfully!");
      setIsError(false);
    } catch (error) {
      setMessage(
        `Error uploading file: ${error.response?.data?.error || error.message}`
      );
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <input
            className="form-input form-input-file"
            type="file"
            accept=".pdf,.csv,.txt"
            onChange={handleFileChange}
          />

          <select
            className="form-select"
            value={dataType}
            onChange={(e) => setDataType(e.target.value)}
          >
            <option value="">Select Type</option>
            {DATA_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <textarea
            className="form-input"
            rows={5}
            cols={60}
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Enter description here"
          />
        </div>

        <button className="form-button" type="submit" disabled={isLoading}>
          {isLoading ? "Uploading..." : "Upload"}
        </button>
      </form>
      <div
        className="loading-indicator"
        style={{ display: isLoading ? "block" : "none" }}
      >
        Loading...
      </div>

      {message && (
        <div style={{ color: isError ? "red" : "green", marginTop: "10px" }}>
          {message}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
