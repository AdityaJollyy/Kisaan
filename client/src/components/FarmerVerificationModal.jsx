import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
    verifyFarmer,
    requestManualVerification,
    clearVerificationError,
    clearVerificationSuccess
} from '../redux/slices/verificationSlice';
import {
    FaTimes,
    FaCheckCircle,
    FaSpinner,
    FaShieldAlt,
    FaFileUpload,
    FaInfoCircle
} from 'react-icons/fa';

const FarmerVerificationModal = ({ isOpen, onClose, onVerificationSuccess }) => {
    const dispatch = useDispatch();
    const { verifying, loading, error, success, verificationMessage } = useSelector(
        (state) => state.verification
    );

    const [currentStep, setCurrentStep] = useState('form'); // 'form', 'success', 'manual'
    const [formData, setFormData] = useState({
        mobile: '',
        aadharLast4: ''
    });
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (success && verificationMessage) {
            setCurrentStep('success');
            setTimeout(() => {
                if (onVerificationSuccess) {
                    onVerificationSuccess();
                }
            }, 2000);
        }
    }, [success, verificationMessage, onVerificationSuccess]);

    const validateForm = () => {
        const newErrors = {};

        if (!formData.mobile) {
            newErrors.mobile = 'Mobile number is required';
        } else if (!/^[6-9]\d{9}$/.test(formData.mobile)) {
            newErrors.mobile = 'Please enter a valid Indian mobile number';
        }

        if (!formData.aadharLast4) {
            newErrors.aadharLast4 = 'Last 4 digits of Aadhar are required';
        } else if (!/^\d{4}$/.test(formData.aadharLast4)) {
            newErrors.aadharLast4 = 'Please enter exactly 4 digits';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        dispatch(verifyFarmer(formData));
    };

    const handleManualVerification = () => {
        dispatch(requestManualVerification());
        setCurrentStep('manual');
    };

    const handleClose = () => {
        setCurrentStep('form');
        setFormData({ mobile: '', aadharLast4: '' });
        setErrors({});
        dispatch(clearVerificationError());
        dispatch(clearVerificationSuccess());
        onClose();
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-200">
                    <div className="flex items-center gap-3">
                        <FaShieldAlt className="text-green-500 text-xl" />
                        <h2 className="text-xl font-semibold text-gray-900">
                            Get Verified
                        </h2>
                    </div>
                    <button
                        onClick={handleClose}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <FaTimes className="text-xl" />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6">
                    {currentStep === 'form' && (
                        <>
                            <div className="mb-6">
                                <div className="flex items-start gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                                    <FaInfoCircle className="text-blue-500 text-lg mt-0.5 flex-shrink-0" />
                                    <div className="text-sm text-blue-800">
                                        <p className="font-medium mb-1">Verification Process</p>
                                        <p>Enter your Aadhar-linked mobile number and last 4 digits of your Aadhar number. This will be verified against government records.</p>
                                    </div>
                                </div>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div>
                                    <label htmlFor="mobile" className="block text-sm font-medium text-gray-700 mb-1">
                                        Aadhar Linked Mobile Number *
                                    </label>
                                    <input
                                        type="tel"
                                        id="mobile"
                                        name="mobile"
                                        value={formData.mobile}
                                        onChange={handleInputChange}
                                        placeholder="Enter 10-digit mobile number"
                                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 ${errors.mobile ? 'border-red-500' : 'border-gray-300'
                                            }`}
                                        maxLength="10"
                                    />
                                    {errors.mobile && (
                                        <p className="text-red-500 text-xs mt-1">{errors.mobile}</p>
                                    )}
                                </div>

                                <div>
                                    <label htmlFor="aadharLast4" className="block text-sm font-medium text-gray-700 mb-1">
                                        Last 4 Digits of Aadhar Number *
                                    </label>
                                    <input
                                        type="text"
                                        id="aadharLast4"
                                        name="aadharLast4"
                                        value={formData.aadharLast4}
                                        onChange={handleInputChange}
                                        placeholder="XXXX"
                                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 ${errors.aadharLast4 ? 'border-red-500' : 'border-gray-300'
                                            }`}
                                        maxLength="4"
                                    />
                                    {errors.aadharLast4 && (
                                        <p className="text-red-500 text-xs mt-1">{errors.aadharLast4}</p>
                                    )}
                                </div>

                                {error && (
                                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                                        <p className="text-red-800 text-sm">{error}</p>
                                    </div>
                                )}

                                <div className="flex gap-3 pt-4">
                                    <button
                                        type="submit"
                                        disabled={verifying}
                                        className="flex-1 flex items-center justify-center gap-2 bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                                    >
                                        {verifying ? (
                                            <>
                                                <FaSpinner className="animate-spin" />
                                                Verifying...
                                            </>
                                        ) : (
                                            <>
                                                <FaCheckCircle />
                                                Verify Now
                                            </>
                                        )}
                                    </button>
                                    <button
                                        type="button"
                                        onClick={handleClose}
                                        className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>

                            <div className="mt-6 pt-6 border-t border-gray-200">
                                <p className="text-sm text-gray-600 mb-3">
                                    Having trouble with automatic verification?
                                </p>
                                <button
                                    onClick={handleManualVerification}
                                    className="w-full flex items-center justify-center gap-2 bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors"
                                >
                                    <FaFileUpload />
                                    Request Manual Verification
                                </button>
                            </div>
                        </>
                    )}

                    {currentStep === 'success' && (
                        <div className="text-center py-8">
                            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                                <FaCheckCircle className="text-green-500 text-2xl" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                Verification Successful!
                            </h3>
                            <p className="text-gray-600 mb-4">
                                {verificationMessage || 'You are now a verified farmer on Kisaan platform.'}
                            </p>
                            <button
                                onClick={handleClose}
                                className="bg-green-500 text-white py-2 px-6 rounded-lg hover:bg-green-600 transition-colors"
                            >
                                Continue
                            </button>
                        </div>
                    )}

                    {currentStep === 'manual' && (
                        <div className="text-center py-8">
                            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                                <FaFileUpload className="text-blue-500 text-2xl" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                Manual Verification Requested
                            </h3>
                            <p className="text-gray-600 mb-4">
                                Our team will review your documents within 2-3 business days. You'll be notified once the verification is complete.
                            </p>
                            <button
                                onClick={handleClose}
                                className="bg-blue-500 text-white py-2 px-6 rounded-lg hover:bg-blue-600 transition-colors"
                            >
                                Got It
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FarmerVerificationModal;
