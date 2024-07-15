// components/Uploader.tsx

import React, { useState } from 'react';
import axios from 'axios';
import { Button, Input } from '@nextui-org/react';

interface UploaderProps {
  onUploadSuccess: () => void;
}

const Uploader: React.FC<UploaderProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onUploadSuccess();
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="mb-4">
      <Input type="file" onChange={handleFileChange} />
      <Button onClick={handleFileUpload} className="mt-2">Upload CSV</Button>
    </div>
  );
};

export default Uploader;
