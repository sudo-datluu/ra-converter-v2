"use client"

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Uploader from './components/Uploader';
import Files from './components/Files';
import FileDetailModal from './components/FileDetailModal';

interface File {
  id: number;
  name: string;
  uploaded_at: string;
}

// const Home: React.FC = () => {
//   return (
//     <section>
//       <div className="container mx-auto px-4">
//         <h1 className="text-4xl font-bold py-4">File Upload</h1>

//       </div>
//     </section>
//   );
// }

// export default Home;

export default async function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [showModal, setShowModal] = useState(false);

  const fetchFiles = () => {
    axios.get('http://localhost:8000/api/files/')
      .then(response => setFiles(response.data))
      .catch(error => console.error('Error fetching files:', error));
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleFileClick = (file: File) => {
    setSelectedFile(file);
    setShowModal(true);
  };

  const handleHideModal = () => {
    setShowModal(false);
    setSelectedFile(null);
  };

  return (
    <section>
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold py-4">File Upload</h1>
        <Uploader onUploadSuccess={fetchFiles} />
        <Files files={files} onFileClick={handleFileClick} />
      </div>
    </section>
  );
}
