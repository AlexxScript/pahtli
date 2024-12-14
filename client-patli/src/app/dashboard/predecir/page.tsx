'use client'
import { FileUpload } from "@/components/predecir/FileUpload";
import { FormPredecir } from "@/components/predecir/FormPredecir";

export const DashboardPredecir = () => {

    return (
        <>
           <FormPredecir/> 
            <FileUpload/>
        </>
        
    );
};

export default DashboardPredecir