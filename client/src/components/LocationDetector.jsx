import { useState } from 'react';
import { FaLocationArrow } from 'react-icons/fa';

/**
 * LocationDetector Component
 * 
 * This component provides a button to detect the user's current location
 * and autofill the address fields (city, state, zipCode) using the browser's
 * Geolocation API and a reverse geocoding service.
 * 
 * @param {Function} onLocationDetected - Callback function that receives the location data
 * @param {Boolean} isLoading - Optional prop to show loading state
 * @returns {JSX.Element} - A location detection button component
 */
const LocationDetector = ({ onLocationDetected, isLoading = false }) => {
    const [detectingLocation, setDetectingLocation] = useState(false);
    const [error, setError] = useState(null);

    const detectLocation = async () => {
        setError(null);
        setDetectingLocation(true);

        try {
            // Check if geolocation is supported by the browser
            if (!navigator.geolocation) {
                throw new Error('Geolocation is not supported by your browser');
            }

            // Get current position
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                });
            });

            const { latitude, longitude } = position.coords;

            // Use reverse geocoding to get address details
            // Using OpenStreetMap's Nominatim service (free, no API key required)
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`
            );

            if (!response.ok) {
                throw new Error('Failed to get address from coordinates');
            }

            const data = await response.json();
            const address = data.address;

            // Extract relevant address components
            const locationData = {
                city: address.city || address.town || address.village || address.county || '',
                state: address.state || '',
                zipCode: address.postcode || '',
                coordinates: {
                    lat: latitude,
                    lng: longitude
                },
                locationDetected: true
            };

            // Call the callback function with the detected location
            onLocationDetected(locationData);
        } catch (err) {
            console.error('Error detecting location:', err);
            setError(err.message || 'Error detecting your location');
        } finally {
            setDetectingLocation(false);
        }
    };

    return (
        <div className="relative">
            <button
                type="button"
                onClick={detectLocation}
                disabled={detectingLocation || isLoading}
                className={`flex items-center gap-1 px-3 py-1.5 text-sm font-medium rounded-md 
          ${detectingLocation || isLoading ? 'bg-gray-300 text-gray-500' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'} 
          transition-colors duration-200`}
                title="Detect my current location"
            >
                <FaLocationArrow className={detectingLocation ? 'animate-pulse' : ''} />
                {detectingLocation ? 'Detecting...' : 'Detect Location'}
            </button>

            {error && (
                <div className="absolute top-full left-0 mt-1 w-48 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-600">
                    {error}
                </div>
            )}
        </div>
    );
};

export default LocationDetector;
