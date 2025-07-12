const MockGovernmentData = require("../models/MockGovernmentDataModel");
const FarmerProfile = require("../models/FarmerProfileModel");
const User = require("../models/UserModel");

// @desc    Verify farmer using government data
// @route   POST /api/verification/verify-farmer
// @access  Private (Farmer only)
exports.verifyFarmer = async (req, res) => {
    try {
        const { mobile, aadharLast4 } = req.body;

        // Validate input
        if (!mobile || !aadharLast4) {
            return res.status(400).json({
                success: false,
                message: "Please provide mobile number and last 4 digits of Aadhar"
            });
        }

        // Validate mobile number format
        if (!/^[6-9]\d{9}$/.test(mobile)) {
            return res.status(400).json({
                success: false,
                message: "Please provide a valid Indian mobile number"
            });
        }

        // Validate aadhar last 4 digits
        if (!/^\d{4}$/.test(aadharLast4)) {
            return res.status(400).json({
                success: false,
                message: "Please provide exactly 4 digits of Aadhar number"
            });
        }

        // Check if farmer is already verified
        const existingProfile = await FarmerProfile.findOne({ user: req.user._id });
        if (existingProfile && existingProfile.isVerified) {
            return res.status(400).json({
                success: false,
                message: "Farmer is already verified"
            });
        }

        // Verify farmer against government data
        const verificationResult = await MockGovernmentData.verifyFarmer(mobile, aadharLast4);

        if (!verificationResult.success) {
            return res.status(400).json({
                success: false,
                message: verificationResult.message || "Verification failed. Please check your details."
            });
        }

        // Update farmer profile with verification status
        let farmerProfile = existingProfile;
        if (!farmerProfile) {
            // Create a basic profile if it doesn't exist
            farmerProfile = await FarmerProfile.create({
                user: req.user._id,
                farmName: req.user.name + "'s Farm",
                description: "Farm description will be updated soon.",
                isVerified: true,
                verificationDetails: {
                    method: 'government_data',
                    verifiedAt: new Date(),
                    verifiedBy: 'system',
                    governmentData: {
                        name: verificationResult.farmer.name,
                        mobile: verificationResult.farmer.mobile,
                        pmKisanId: verificationResult.farmer.pmKisanId
                    }
                }
            });
        } else {
            farmerProfile.isVerified = true;
            farmerProfile.verificationDetails = {
                method: 'government_data',
                verifiedAt: new Date(),
                verifiedBy: 'system',
                governmentData: {
                    name: verificationResult.farmer.name,
                    mobile: verificationResult.farmer.mobile,
                    pmKisanId: verificationResult.farmer.pmKisanId
                }
            };
            await farmerProfile.save();
        }

        res.json({
            success: true,
            message: "Farmer verified successfully!",
            data: {
                isVerified: true,
                farmer: verificationResult.farmer
            }
        });

    } catch (error) {
        console.error("Error verifying farmer:", error);
        res.status(500).json({
            success: false,
            message: "Server error during verification",
            error: error.message
        });
    }
};

// @desc    Get farmer verification status
// @route   GET /api/verification/status
// @access  Private (Farmer only)
exports.getVerificationStatus = async (req, res) => {
    try {
        const farmerProfile = await FarmerProfile.findOne({ user: req.user._id });

        res.json({
            success: true,
            data: {
                isVerified: farmerProfile ? farmerProfile.isVerified : false,
                hasProfile: !!farmerProfile
            }
        });
    } catch (error) {
        console.error("Error getting verification status:", error);
        res.status(500).json({
            success: false,
            message: "Server error",
            error: error.message
        });
    }
};

// @desc    Request manual verification (for future implementation)
// @route   POST /api/verification/manual-request
// @access  Private (Farmer only)
exports.requestManualVerification = async (req, res) => {
    try {
        // This is a placeholder for future manual verification implementation
        // For now, we'll just log the request and return a message

        console.log(`Manual verification requested by user: ${req.user._id}`);

        res.json({
            success: true,
            message: "Manual verification request submitted. Our team will review your documents within 2-3 business days."
        });
    } catch (error) {
        console.error("Error requesting manual verification:", error);
        res.status(500).json({
            success: false,
            message: "Server error",
            error: error.message
        });
    }
};

// @desc    Get verification statistics (Admin only)
// @route   GET /api/verification/stats
// @access  Private (Admin only)
exports.getVerificationStats = async (req, res) => {
    try {
        const govStats = await MockGovernmentData.getVerificationStats();

        const farmerStats = await FarmerProfile.aggregate([
            {
                $group: {
                    _id: null,
                    totalFarmers: { $sum: 1 },
                    verifiedFarmers: {
                        $sum: { $cond: ["$isVerified", 1, 0] }
                    }
                }
            }
        ]);

        const stats = farmerStats[0] || { totalFarmers: 0, verifiedFarmers: 0 };

        res.json({
            success: true,
            data: {
                farmers: {
                    total: stats.totalFarmers,
                    verified: stats.verifiedFarmers,
                    unverified: stats.totalFarmers - stats.verifiedFarmers,
                    verificationRate: stats.totalFarmers > 0 ? ((stats.verifiedFarmers / stats.totalFarmers) * 100).toFixed(2) : 0
                },
                government: govStats
            }
        });
    } catch (error) {
        console.error("Error getting verification stats:", error);
        res.status(500).json({
            success: false,
            message: "Server error",
            error: error.message
        });
    }
};
