import { FaRobot } from "react-icons/fa";
import { useSelector } from "react-redux";
import { useNavigate, useLocation } from "react-router-dom";

const AIAssistantFab = () => {
    const { isAuthenticated, user } = useSelector((state) => state.auth);
    const navigate = useNavigate();
    const location = useLocation();

    // Only show for farmers and not on the AI Assistant page itself
    if (!isAuthenticated || user?.role !== "farmer" || location.pathname === "/farmer/ai-assistant") {
        return null;
    }

    return (
        <button
            className="fixed bottom-6 right-6 z-50 bg-green-600 hover:bg-green-700 text-white rounded-full shadow-lg p-4 flex items-center justify-center transition-colors"
            style={{ boxShadow: "0 4px 16px rgba(0,0,0,0.18)" }}
            aria-label="Open AI Assistant"
            onClick={() => navigate("/farmer/ai-assistant")}
        >
            <FaRobot size={28} />
        </button>
    );
};

export default AIAssistantFab;
