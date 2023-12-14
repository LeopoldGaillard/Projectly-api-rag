import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const [dataType, setDataType] = useState("");
  const DATA_TYPES = [
    "Hourly Cost",
    "Bill",
    "Contract",
    "Order Form",
    "Bank Balance",
    "Other",
  ];

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);
    formData.append("description", description);
    formData.append("dataType", dataType);

    try {
      await axios.post("http://127.0.0.1:5000/projectly/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage("File uploaded successfully!");
      setIsError(false);
    } catch (error) {
      setMessage(
        `Error uploading file: ${error.response?.data?.error || error.message}`
      );
      setIsError(true);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />

        <select value={dataType} onChange={(e) => setDataType(e.target.value)}>
          <option value="">Select Type</option>
          {DATA_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>

        <input
          type="text"
          value={description}
          onChange={handleDescriptionChange}
          placeholder="Enter description here"
        />
        <button type="submit">Upload</button>
      </form>
      {message && (
        <div style={{ color: isError ? "red" : "green", marginTop: "10px" }}>
          {message}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
