import React, { useEffect, useState } from 'react';
import { getEDASummary } from '../services/api';
import { Sparkles, Loader2, BarChart2 } from 'lucide-react';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
    ScatterChart, Scatter, ZAxis
} from 'recharts';

const EDA = () => {
    const [aiReport, setAiReport] = useState<string | null>(null);
    const [loadingAI, setLoadingAI] = useState(false);

    // Mocked correlation data to send to Gemini for the storyteller
    const mockCorrelationData = {
        "radius_mean": { "perimeter_mean": 0.99, "area_mean": 0.98, "compactness_mean": 0.50 },
        "texture_mean": { "smoothness_mean": -0.02, "symmetry_mean": 0.07 },
        "notes": "Variáveis de dimensão (radius, perimeter, area) possuem correlação altíssima."
    };

    const chartData = [
        { name: 'Maligno (M)', count: 212, fill: '#ef4444' },
        { name: 'Benigno (B)', count: 357, fill: '#10b981' }
    ];

    const fetchAiReport = async () => {
        setLoadingAI(true);
        try {
            const response = await getEDASummary(mockCorrelationData);
            setAiReport(response.data.story);
        } catch (error) {
            console.error("Erro AI", error);
            setAiReport("Erro: Não foi possível gerar o storytelling devido a um erro de comunicação com a API do Gemini.");
        } finally {
            setLoadingAI(false);
        }
    };

    useEffect(() => {
        fetchAiReport();
    }, []);

    return (
        <div className="space-y-6 flex flex-col h-full">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                    <BarChart2 className="text-blue-600" />
                    Análise Exploratória (EDA)
                </h1>
            </div>

            {/* Caixa de AI Insights */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-xl p-6 shadow-sm">
                <div className="flex items-center gap-2 mb-4">
                    <Sparkles className="text-amber-500" size={24} />
                    <h3 className="text-lg font-semibold text-slate-800">IA Generativa: Data Storytelling</h3>
                </div>

                {loadingAI ? (
                    <div className="flex items-center gap-3 text-slate-500">
                        <Loader2 className="animate-spin" />
                        <span>O Gemini está analisando a matriz de correlação estatística...</span>
                    </div>
                ) : (
                    <div className="prose prose-sm prose-slate max-w-none prose-p:leading-relaxed">
                        <p className="text-slate-700 whitespace-pre-wrap">{aiReport}</p>
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1">

                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col">
                    <h4 className="font-medium text-slate-700 mb-6 text-center">Distribuição de Casos (Target)</h4>
                    <div className="flex-1 w-full min-h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                                <XAxis dataKey="name" tick={{ fill: '#64748B' }} tickLine={false} axisLine={false} />
                                <YAxis tick={{ fill: '#64748B' }} tickLine={false} axisLine={false} />
                                <RechartsTooltip cursor={{ fill: '#F1F5F9' }} />
                                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex items-center justify-center text-center">
                    <div className="text-slate-400 max-w-sm">
                        <Database className="mx-auto mb-4 opacity-50" size={48} />
                        <p>Os gráficos de Dispersão (Scatter) e Boxplots comparativos detalhados requerem a conclusão da Fase 5 da Arquitetura pelo Desenvolvedor Front-end.</p>
                    </div>
                </div>

            </div>
        </div>
    );
};

// Simple Mock component to import icon that I missed at the top
const Database = ({ size, className }: { size: number, className: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M3 5V19A9 3 0 0 0 21 19V5" /><path d="M3 12A9 3 0 0 0 21 12" /></svg>
);

export default EDA;
