import React from "react";

interface ModelData {
    Model: string;
    Accuracy_score: number;
    Precision_scores: number;
    Recall_scores: number;
    F1_scores: number;
    AUC_scores: number;
}

const Table: React.FC = () => {
    const data: ModelData[] = [
        { Model: "DecisionTreeClassifier", Accuracy_score: 0.831522, Precision_scores: 0.887755, Recall_scores: 0.813084, F1_scores: 0.848780, AUC_scores: 0.835113 },
        { Model: "Regression", Accuracy_score: 0.842391, Precision_scores: 0.906250, Recall_scores: 0.813084, F1_scores: 0.857143, AUC_scores: 0.848100 },
        { Model: "SVM", Accuracy_score: 0.842391, Precision_scores: 0.906250, Recall_scores: 0.813084, F1_scores: 0.857143, AUC_scores: 0.848100 },
        { Model: "RandomForest", Accuracy_score: 0.880435, Precision_scores: 0.938144, Recall_scores: 0.850467, F1_scores: 0.892157, AUC_scores: 0.886273 },
    ];

    return (
        <div className="overflow-x-auto">
            <h2 className="font-semibold text-[#84D5C0] my-4 text-center">Tabla comparativa del rendimiento de los modelos</h2>
            <table className="min-w-full border-collapse border border-gray-900">
                <thead>
                    <tr className="bg-[#202020]">
                        <th className="border border-[#404040] px-4 py-2 text-left">Model</th>
                        <th className="border border-[#404040] px-4 py-2 text-left">Accuracy Score</th>
                        <th className="border border-[#404040] px-4 py-2 text-left">Precision Score</th>
                        <th className="border border-[#404040] px-4 py-2 text-left">Recall Score</th>
                        <th className="border border-[#404040] px-4 py-2 text-left">F1 Score</th>
                        <th className="border border-[#404040] px-4 py-2 text-left">AUC Score</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index} className={index % 2 === 0 ? "bg-[#303030]" : "bg-[#505050]"}>
                            <td className="border border-[#404040] px-4 py-2">{row.Model}</td>
                            <td className="border border-[#404040] px-4 py-2">{row.Accuracy_score.toFixed(6)}</td>
                            <td className="border border-[#404040] px-4 py-2">{row.Precision_scores.toFixed(6)}</td>
                            <td className="border border-[#404040] px-4 py-2">{row.Recall_scores.toFixed(6)}</td>
                            <td className="border border-[#404040] px-4 py-2">{row.F1_scores.toFixed(6)}</td>
                            <td className="border border-[#404040] px-4 py-2">{row.AUC_scores.toFixed(6)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Table;
