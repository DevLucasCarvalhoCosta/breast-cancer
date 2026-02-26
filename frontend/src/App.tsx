import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import DataExplorer from './pages/DataExplorer';
import EDA from './pages/EDA';
import Predict from './pages/Predict';
import Models from './pages/Models';

// No placeholders anymore

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="data" element={<DataExplorer />} />
          <Route path="eda" element={<EDA />} />
          <Route path="models" element={<Models />} />
          <Route path="predict" element={<Predict />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
