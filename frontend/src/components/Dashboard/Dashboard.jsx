import React, { useContext, useEffect } from "react";
import { UploadContext } from "../../context/UploadContext";

export default function Dashboard() {
    const { rfmData } = useContext(UploadContext);

    useEffect(() => {
        console.log("Dashboard Loaded - RFM Data:", rfmData);
    }, [rfmData]); // تشغيل عند تغيير البيانات

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
            {rfmData ? (
                <pre className="bg-gray-200 p-4 rounded">{JSON.stringify(rfmData, null, 2)}</pre>
            ) : (
                <p>No data available. Please upload a file first.</p>
            )}
        </div>
    );
}
