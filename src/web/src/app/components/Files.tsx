// components/Files.tsx

import React from 'react';
import {  
    Table,  
    TableHeader,  
    TableBody,  
    TableColumn,  
    TableRow,  
    TableCell
} from "@nextui-org/react";

interface File {
  id: number;
  name: string;
  uploaded_at: string;
}

interface FilesProps {
  files: File[];
  onFileClick: (file: File) => void;
}

const Files: React.FC<FilesProps> = ({ files, onFileClick }) => {
  return (
    <Table>
      <TableHeader>
        <TableColumn>ID</TableColumn>
        <TableColumn>Name</TableColumn>
        <TableColumn>Uploaded At</TableColumn>
      </TableHeader>
      <TableBody>
        {files.map(file => (
          <TableRow key={file.id} onClick={() => onFileClick(file)}>
            <TableCell>{file.id}</TableCell>
            <TableCell>{file.name}</TableCell>
            <TableCell>{file.uploaded_at}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default Files;
