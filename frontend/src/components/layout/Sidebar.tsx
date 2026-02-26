import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Database, BarChart2, CheckSquare, Stethoscope } from 'lucide-react';

const Sidebar = () => {
    const menuItems = [
        { path: '/', name: 'Dashboard Geral', icon: <LayoutDashboard size={20} /> },
        { path: '/data', name: 'Explorador de Dados', icon: <Database size={20} /> },
        { path: '/eda', name: 'Análise Exploratória', icon: <BarChart2 size={20} /> },
        { path: '/models', name: 'Comparação de Modelos', icon: <CheckSquare size={20} /> },
        { path: '/predict', name: 'Predição Online', icon: <Stethoscope size={20} /> },
    ];

    return (
        <div className="flex flex-col w-64 h-screen bg-slate-900 border-r border-slate-700 text-slate-300">
            <div className="flex items-center justify-center h-20 border-b border-slate-700">
                <h1 className="text-2xl font-bold text-white tracking-wider flex items-center gap-2">
                    <Stethoscope className="text-rose-500" />
                    CancerMama
                </h1>
            </div>
            <div className="flex-1 overflow-y-auto py-4">
                <ul className="space-y-2">
                    {menuItems.map((item) => (
                        <li key={item.name} className="px-4">
                            <NavLink
                                to={item.path}
                                className={({ isActive }) =>
                                    `flex items-center space-x-3 p-3 rounded-lg transition-colors ${isActive
                                        ? 'bg-rose-600/20 text-rose-400 border border-rose-600/30'
                                        : 'hover:bg-slate-800 hover:text-white'
                                    }`
                                }
                            >
                                {item.icon}
                                <span className="font-medium">{item.name}</span>
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="p-4 border-t border-slate-700 text-xs text-center text-slate-500">
                Desenvolvido com IA <br /> Powered by Google Cloud
            </div>
        </div>
    );
};

export default Sidebar;
