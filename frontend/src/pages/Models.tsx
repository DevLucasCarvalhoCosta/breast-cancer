import { CheckSquare } from 'lucide-react';

const Models = () => {
    return (
        <div className="space-y-6">
            <div className="flex items-center gap-3 mb-8">
                <CheckSquare className="text-indigo-600" size={32} />
                <div>
                    <h1 className="text-2xl font-bold text-slate-800">Comparação de Modelos ML</h1>
                    <p className="text-slate-500">Avaliação de performance dos modelos scikit-learn treinados.</p>
                </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-xl p-12 shadow-sm text-center">
                <div className="max-w-md mx-auto space-y-4">
                    <h3 className="text-xl font-medium text-slate-700">Painel de Métricas</h3>
                    <p className="text-slate-500">
                        Esta tela hospedará as visualizações de Matriz de Confusão e Curva ROC comparando Support Vector Machine (SVM), Random Forest e Regressão Logística.
                        (Fase 5 do Desenvolvimento).
                    </p>
                    <div className="pt-6">
                        <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                            <div className="h-full bg-indigo-500 w-1/3 animate-pulse"></div>
                        </div>
                        <span className="text-xs text-slate-400 mt-2 block">Pendente de refatoração do backend ml_service</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Models;
