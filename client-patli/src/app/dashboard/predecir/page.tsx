'use client'
import { FileUpload } from "@/components/predecir/FileUpload";
import { FormPredecir } from "@/components/predecir/FormPredecir";
import { useAuth } from "@/hooks/useAuth"
import { useEffect, useState } from "react";

export const DashboardPredecir = () => {

    return (
        <>
           <FormPredecir/> 
            <FileUpload/>
        </>
        
    );
};

export default DashboardPredecir