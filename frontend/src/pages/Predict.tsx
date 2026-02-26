import { useState } from 'react';
import { getMedicalReport } from '../services/api';
import { Stethoscope, Loader2, FileText, AlertTriangle } from 'lucide-react';

const Predict = () => {
    const [loading, setLoading] = useState(false);
    const [report, setReport] = useState<string | null>(null);

    // Minimal form state to trigger the AI for demonstration
    // In a real scenario, this would have 30 inputs for all features
    const [formData, setFormData] = useState({
        radius_mean: 17.99,
        texture_mean: 10.38,
        area_mean: 1001.0,
        smoothness_mean: 0.1184,
    });

    const handlePredict = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setReport(null);

        try {
            // Simulando a predição do modelo de ML (neste caso, Forçando Maligno para fins de teste da IA explicável)
            const mockPrediction = 1;
            const mockProbability = 0.92;

            const response = await getMedicalReport({
                features_data: formData,
                prediction: mockPrediction,
                probability: mockProbability
            });

            setReport(response.data.report);
        } catch (err) {
            console.error(err);
            setReport("Erro ao se conectar com a API do Gemini. Verifique se a chave GEMINI_API_KEY está configurada no backend.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6 h-full pb-10">
            <div className="flex items-center gap-3 mb-8">
                <Stethoscope className="text-rose-600" size={32} />
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Predição com IA Explicável</h1>
                    <p className="text-slate-500">Insira os dados celulares para receber o laudo gerado pelo Gemini.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Formulário */}
                <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
                    <h3 className="text-lg font-medium text-slate-800 mb-4 border-b pb-2">Dados do Paciente</h3>
                    <form onSubmit={handlePredict} className="space-y-4">

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Raio Médio (radius_mean)</label>
                            <input type="number" step="0.01" value={formData.radius_mean} onChange={e => setFormData({ ...formData, radius_mean: parseFloat(e.target.value) })}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Textura Média (texture_mean)</label>
                            <input type="number" step="0.01" value={formData.texture_mean} onChange={e => setFormData({ ...formData, texture_mean: parseFloat(e.target.value) })}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Área Média (area_mean)</label>
                            <input type="number" step="0.01" value={formData.area_mean} onChange={e => setFormData({ ...formData, area_mean: parseFloat(e.target.value) })}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none"
                            />
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit" disabled={loading}
                                className="w-full bg-rose-600 hover:bg-rose-700 text-white font-medium py-2 px-4 rounded-lg flex justify-center items-center gap-2 transition-colors disabled:opacity-70"
                            >
                                {loading ? <Loader2 className="animate-spin" size={20} /> : <FileText size={20} />}
                                {loading ? 'Consultando ML e Gemini...' : 'Gerar Diagnóstico IA'}
                            </button>
                        </div>
                    </form>

                    <div className="mt-6 p-4 bg-amber-50 rounded-lg border border-amber-200 flex items-start gap-3">
                        <AlertTriangle className="text-amber-600 mt-0.5" size={20} />
                        <p className="text-xs text-amber-800">
                            Nota: Para fins da Fase 6, apenas 3 features estão mapeadas na UI. O backend processa o prompt completo.
                        </p>
                    </div>
                </div>

                {/* Resultado */}
                <div className="bg-white border border-slate-200 rounded-xl shadow-sm flex flex-col overflow-hidden">
                    <div className="bg-slate-50 border-b border-slate-200 p-4 shrink-0">
                        <h3 className="font-medium text-slate-800">Laudo Médico (Gemini 2.5)</h3>
                    </div>

                    <div className="p-6 flex-1 overflow-y-auto bg-slate-50/50">
                        {loading ? (
                            <div className="h-full flex flex-col items-center justify-center text-slate-400 gap-3">
                                <Loader2 className="animate-spin text-rose-500" size={32} />
                                <p>A inteligência artificial está escrevendo o laudo explicativo...</p>
                            </div>
                        ) : report ? (
                            <div className="prose prose-sm prose-slate max-w-none prose-p:leading-relaxed whitespace-pre-wrap">
                                {report}
                            </div>
                        ) : (
                            <div className="h-full flex flex-col items-center justify-center text-slate-400 gap-3 text-center">
                                <FileText size={48} className="opacity-20" />
                                <p>O laudo aparecerá aqui após a submissão dos dados clinicos.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Predict;
