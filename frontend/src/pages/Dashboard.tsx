

const Dashboard = () => {
    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-slate-900">Dashboard Geral</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Metric Cards will go here */}
                <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col">
                    <span className="text-sm font-medium text-slate-500">Total de Amostras</span>
                    <span className="text-3xl font-bold text-slate-800 mt-2">569</span>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col">
                    <span className="text-sm font-medium text-slate-500">Maligno</span>
                    <span className="text-3xl font-bold text-rose-600 mt-2">212 (37.3%)</span>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col">
                    <span className="text-sm font-medium text-slate-500">Benigno</span>
                    <span className="text-3xl font-bold text-emerald-600 mt-2">357 (62.7%)</span>
                </div>

                <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6 flex flex-col">
                    <span className="text-sm font-medium text-slate-500">Features Preditivas</span>
                    <span className="text-3xl font-bold text-indigo-600 mt-2">30</span>
                </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-8 text-center mt-12">
                <h3 className="text-xl font-medium text-slate-700 mb-2">Bem-vindo ao CancerMama AI Pipeline</h3>
                <p className="text-slate-500 max-w-2xl mx-auto">
                    Navegue pelo menu lateral para explorar as distribuições clínicas, entender as correlações com a assistência de I.A. (Gemini) e avaliar os modelos de Machine Learning.
                </p>
            </div>
        </div>
    );
};

export default Dashboard;
