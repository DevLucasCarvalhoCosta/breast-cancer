import { useEffect, useState } from 'react';
import { getSamples, getFeatures } from '../services/api';
import type { SampleWithFeatures, FeatureDefinitionResponse } from '../types';
import { Loader2, Search } from 'lucide-react';

const DataExplorer = () => {
    const [samples, setSamples] = useState<SampleWithFeatures[]>([]);
    const [features, setFeatures] = useState<FeatureDefinitionResponse[]>([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [samplesRes, featuresRes] = await Promise.all([
                    getSamples({ page, page_size: 15, diagnosis: filter || undefined }),
                    getFeatures()
                ]);
                setSamples(samplesRes.data.items);
                setTotalPages(samplesRes.data.total_pages);
                setFeatures(featuresRes.data);
            } catch (err) {
                console.error("Erro ao carregar dados", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [page, filter]);

    // Pegamos apenas as 5 primeiras features para não quebrar a tabela visivelmente
    const displayFeatures = features.slice(0, 5);

    return (
        <div className="space-y-6 flex flex-col h-full">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-slate-800">Dataset de Tumores da Mama</h1>
                <div className="flex gap-2 relative">
                    <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                        <Search size={16} className="text-slate-400" />
                    </div>
                    <select
                        className="pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm bg-white focus:ring-2 focus:ring-rose-500 outline-none"
                        value={filter}
                        onChange={(e) => { setFilter(e.target.value); setPage(1); }}
                    >
                        <option value="">Todos os Diagnósticos</option>
                        <option value="M">Maligno (M)</option>
                        <option value="B">Benigno (B)</option>
                    </select>
                </div>
            </div>

            <div className="bg-white border border-slate-200 shadow-sm rounded-xl overflow-hidden flex-1 flex flex-col">
                <div className="overflow-x-auto flex-1">
                    <table className="w-full text-left text-sm text-slate-600">
                        <thead className="bg-slate-50 border-b border-slate-200 text-slate-700">
                            <tr>
                                <th className="px-6 py-3 font-medium">Original ID</th>
                                <th className="px-6 py-3 font-medium">Diagnóstico</th>
                                {displayFeatures.map(f => (
                                    <th key={f.name} className="px-6 py-3 font-medium" title={f.description}>
                                        {f.name}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {loading ? (
                                <tr>
                                    <td colSpan={7} className="text-center py-20">
                                        <Loader2 className="animate-spin mx-auto text-rose-500 mb-2" />
                                        Carregando amostras...
                                    </td>
                                </tr>
                            ) : samples.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="text-center py-20 text-slate-500">
                                        Nenhuma amostra encontrada. O ETL já foi rodado?
                                    </td>
                                </tr>
                            ) : (
                                samples.map(sample => (
                                    <tr key={sample.id} className="hover:bg-slate-50">
                                        <td className="px-6 py-4 font-mono text-xs">{sample.original_id}</td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${sample.diagnosis === 'M' ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'
                                                }`}>
                                                {sample.diagnosis === 'M' ? 'Maligno' : 'Benigno'}
                                            </span>
                                        </td>
                                        {displayFeatures.map(f => (
                                            <td key={f.name} className="px-6 py-4">
                                                {sample.features[f.name]?.toFixed(4) || '-'}
                                            </td>
                                        ))}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>

                {/* Paginação */}
                <div className="border-t border-slate-200 px-6 py-4 flex items-center justify-between bg-slate-50 mt-auto">
                    <span className="text-sm text-slate-500">
                        Página <span className="font-medium text-slate-800">{page}</span> de <span className="font-medium text-slate-800">{totalPages}</span>
                    </span>
                    <div className="flex gap-2">
                        <button
                            disabled={page === 1 || loading}
                            onClick={() => setPage(p => p - 1)}
                            className="px-3 py-1 text-sm bg-white border border-slate-200 rounded shadow-sm hover:bg-slate-100 disabled:opacity-50"
                        >
                            Anterior
                        </button>
                        <button
                            disabled={page === totalPages || loading}
                            onClick={() => setPage(p => p + 1)}
                            className="px-3 py-1 text-sm bg-white border border-slate-200 rounded shadow-sm hover:bg-slate-100 disabled:opacity-50"
                        >
                            Próxima
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DataExplorer;
