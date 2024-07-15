// components/FileDetailModaltsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Import modal components from NextUI
import {
    Modal, 
    ModalContent, 
    ModalHeader, 
    ModalBody, 
    ModalFooter,
} from "@nextui-org/react";

// Import table components from NextUI
import {
    Table,  
    TableHeader,  
    TableBody,  
    TableColumn,  
    TableRow,  
    TableCell
} from "@nextui-org/react";

// Import dropdown components from NextUI
import {
    Dropdown,
    DropdownTrigger,
    DropdownMenu,
    DropdownSection,
    DropdownItem,
    Button
} from '@nextui-org/react';

interface Column {
  id: number;
  column_name: string;
  column_type: string;
}

interface FileDetailModalProps {
  show: boolean;
  file: { id: number; name: string } | null;
  onHide: () => void;
}

const FileDetailModal: React.FC<FileDetailModalProps> = ({ show, file, onHide }) => {
  const [columns, setColumns] = useState<Column[]>([]);
  const [editedColumns, setEditedColumns] = useState<{ [key: number]: string }>({});

  useEffect(() => {
    if (file) {
      axios.get(`http://localhost:8000/api/columns/${file.id}/`)
        .then(response => setColumns(response.data))
        .catch(error => console.error('Error fetching columns:', error));
    }
  }, [file]);

  const handleColumnTypeChange = (columnId: number, newType: string) => {
    setEditedColumns({
      ...editedColumns,
      [columnId]: newType,
    });
  };

  const handleSaveChanges = async () => {
    for (const columnId in editedColumns) {
      try {
        await axios.post(`http://localhost:8000/api/update-column-type/${columnId}/`, {
          column_type: editedColumns[columnId],
        });
      } catch (error) {
        console.error('Error updating column type:', error);
      }
    }
    onHide();
  };

  return (
    <Modal isOpen={show} onClose={onHide}>
      <ModalHeader>
        <span>File Details</span>
      </ModalHeader>
      <ModalBody>
        {file && (
          <div>
            <h5>File Name: {file.name}</h5>
            <Table>
              <TableHeader>
                <TableColumn>Column Name</TableColumn>
                <TableColumn>Column Type</TableColumn>
                <TableColumn>New Column Type</TableColumn>
              </TableHeader>
              <TableBody>
                {columns.map(col => (
                  <TableRow key={col.id}>
                    <TableCell>{col.column_name}</TableCell>
                    <TableCell>{col.column_type}</TableCell>
                    <TableCell>
                      <Dropdown>
                        <DropdownTrigger>
                            <Button>{col.column_type}</Button>
                        </DropdownTrigger>
                        <DropdownMenu
                          onAction={(key) => handleColumnTypeChange(col.id, key.toString())}
                        >
                          <DropdownItem key="Number">Number</DropdownItem>
                          <DropdownItem key="String">String</DropdownItem>
                          <DropdownItem key="Datetime">Datetime</DropdownItem>
                          <DropdownItem key="Complex">Complex</DropdownItem>
                        </DropdownMenu>
                      </Dropdown>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </ModalBody>
      <ModalFooter>
        <Button onClick={onHide}>
          Close
        </Button>
        <Button onClick={handleSaveChanges}>
          Save Changes
        </Button>
      </ModalFooter>
    </Modal>
  );
};

export default FileDetailModal;
