import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const Layout = () => {
    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col h-screen overflow-hidden">
                <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm">
                    <h2 className="text-xl font-semibold text-slate-800">ML Pipeline Analysis</h2>
                    <div className="flex items-center gap-4">
                        <div className="text-sm font-medium px-3 py-1 bg-blue-50 text-blue-600 rounded-full border border-blue-200">
                            Ambiente: Desenvolvimento
                        </div>
                    </div>
                </header>
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-slate-50 p-6">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;
