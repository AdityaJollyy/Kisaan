import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllFarmers } from "../redux/slices/farmerSlice";
import FarmerCard from "../components/FarmerCard";
import Loader from "../components/Loader";
import {
  FaSearch,
  FaLeaf,
  FaFilter,
  FaTimes,
  FaCheckCircle,
} from "react-icons/fa";

const FarmersPage = () => {
  const dispatch = useDispatch();
  const { farmers, loading } = useSelector((state) => state.farmers);

  const [searchTerm, setSearchTerm] = useState("");
  const [verificationFilter, setVerificationFilter] = useState("all"); // 'all', 'verified', 'unverified'
  const [sortBy, setSortBy] = useState("name"); // 'name', 'verified', 'createdAt'
  const [sortOrder, setSortOrder] = useState("asc");
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    // Build query parameters
    const params = new URLSearchParams();

    if (verificationFilter !== "all") {
      params.append("verified", verificationFilter === "verified");
    }
    if (searchTerm.trim()) {
      params.append("search", searchTerm.trim());
    }
    params.append("sortBy", sortBy);
    params.append("order", sortOrder);

    // Dispatch with query string
    dispatch(getAllFarmers(params.toString() ? `?${params.toString()}` : ''));
  }, [dispatch, verificationFilter, searchTerm, sortBy, sortOrder]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const clearFilters = () => {
    setSearchTerm("");
    setVerificationFilter("all");
    setSortBy("name");
    setSortOrder("asc");
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="container mx-auto px-4 py-8">      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Our Farmers</h1>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex flex-col lg:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <input
                type="text"
                value={searchTerm}
                onChange={handleSearchChange}
                placeholder="Search farmers by name, location..."
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaSearch className="text-gray-400" />
              </div>
            </div>
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-3 border rounded-lg transition-colors ${showFilters
              ? 'bg-green-50 border-green-300 text-green-700'
              : 'border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
          >
            <FaFilter />
            Filters
          </button>
        </div>

        {/* Filter Options */}
        {showFilters && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Verification Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Verification Status
                </label>
                <select
                  value={verificationFilter}
                  onChange={(e) => setVerificationFilter(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="all">All Farmers</option>
                  <option value="verified">Verified Only</option>
                  <option value="unverified">Unverified Only</option>
                </select>
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort By
                </label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="name">Name</option>
                  <option value="verified">Verification Status</option>
                  <option value="createdAt">Join Date</option>
                </select>
              </div>

              {/* Sort Order */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sort Order
                </label>
                <select
                  value={sortOrder}
                  onChange={(e) => setSortOrder(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  <option value="asc">Ascending</option>
                  <option value="desc">Descending</option>
                </select>
              </div>
            </div>

            {/* Clear Filters */}
            <div className="mt-4">
              <button
                onClick={clearFilters}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                <FaTimes className="text-sm" />
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Active Filters Display */}
      {(searchTerm || verificationFilter !== "all") && (
        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600">Active filters:</span>
            {searchTerm && (
              <span className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                Search: "{searchTerm}"
                <button onClick={() => setSearchTerm("")}>
                  <FaTimes className="text-xs" />
                </button>
              </span>
            )}
            {verificationFilter !== "all" && (
              <span className="inline-flex items-center gap-1 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                {verificationFilter === "verified" ? (
                  <>
                    <FaCheckCircle className="text-xs" />
                    Verified Only
                  </>
                ) : (
                  <>
                    <FaTimes className="text-xs" />
                    Unverified Only
                  </>
                )}
                <button onClick={() => setVerificationFilter("all")}>
                  <FaTimes className="text-xs ml-1" />
                </button>
              </span>
            )}
          </div>
        </div>
      )}

      {/* Results */}
      {farmers && farmers.length > 0 ? (
        <>
          <div className="mb-6">
            <p className="text-gray-600">
              Showing {farmers.length} farmer{farmers.length !== 1 ? 's' : ''}
              {searchTerm && ` matching "${searchTerm}"`}
              {verificationFilter !== "all" && (
                <span className="ml-1">
                  ({verificationFilter === "verified" ? "verified only" : "unverified only"})
                </span>
              )}
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {farmers.map((farmer) => (
              <FarmerCard key={farmer._id} farmer={farmer} />
            ))}
          </div>
        </>
      ) : (
        <div className="text-center py-12">
          <FaLeaf className="text-green-500 text-5xl mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Farmers Found</h3>
          <p className="text-gray-600 mb-4">
            {searchTerm || verificationFilter !== "all"
              ? "Try adjusting your search criteria or filters."
              : "No farmers have joined yet."
            }
          </p>
          {(searchTerm || verificationFilter !== "all") && (
            <button
              onClick={clearFilters}
              className="text-green-600 hover:text-green-700 font-medium"
            >
              Clear all filters
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default FarmersPage;
