import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../utils/axiosConfig';
import { toast } from 'react-toastify';

// Verify farmer using government data
export const verifyFarmer = createAsyncThunk(
    'verification/verifyFarmer',
    async (verificationData, { rejectWithValue }) => {
        try {
            const { data } = await axiosInstance.post('/api/verification/verify-farmer', verificationData);
            return data;
        } catch (error) {
            const message = error.response && error.response.data.message
                ? error.response.data.message
                : error.message;
            return rejectWithValue(message);
        }
    }
);

// Get verification status
export const getVerificationStatus = createAsyncThunk(
    'verification/getStatus',
    async (_, { rejectWithValue, getState }) => {
        try {
            // Check if user is authenticated and is a farmer
            const { auth } = getState();
            if (!auth.isAuthenticated || !auth.token || auth.user?.role !== "farmer") {
                return rejectWithValue("User not authenticated or not a farmer");
            }

            const { data } = await axiosInstance.get('/api/verification/status');
            return data;
        } catch (error) {
            const message = error.response && error.response.data.message
                ? error.response.data.message
                : error.message;
            return rejectWithValue(message);
        }
    }
);

// Request manual verification
export const requestManualVerification = createAsyncThunk(
    'verification/requestManual',
    async (_, { rejectWithValue }) => {
        try {
            const { data } = await axiosInstance.post('/api/verification/manual-request');
            return data;
        } catch (error) {
            const message = error.response && error.response.data.message
                ? error.response.data.message
                : error.message;
            return rejectWithValue(message);
        }
    }
);

const initialState = {
    isVerified: false,
    hasProfile: false,
    loading: false,
    verifying: false,
    error: null,
    success: false,
    verificationMessage: null
};

const verificationSlice = createSlice({
    name: 'verification',
    initialState,
    reducers: {
        clearVerificationError: (state) => {
            state.error = null;
        },
        clearVerificationSuccess: (state) => {
            state.success = false;
            state.verificationMessage = null;
        },
        resetVerificationState: (state) => {
            state.error = null;
            state.success = false;
            state.verificationMessage = null;
            state.verifying = false;
        }
    },
    extraReducers: (builder) => {
        builder
            // Verify farmer
            .addCase(verifyFarmer.pending, (state) => {
                state.verifying = true;
                state.error = null;
                state.success = false;
            })
            .addCase(verifyFarmer.fulfilled, (state, action) => {
                state.verifying = false;
                state.success = true;
                state.isVerified = action.payload.data.isVerified;
                state.verificationMessage = action.payload.message;
                toast.success(action.payload.message || 'Farmer verified successfully!');
            })
            .addCase(verifyFarmer.rejected, (state, action) => {
                state.verifying = false;
                state.error = action.payload;
                toast.error(action.payload || 'Verification failed');
            })

            // Get verification status
            .addCase(getVerificationStatus.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(getVerificationStatus.fulfilled, (state, action) => {
                state.loading = false;
                state.isVerified = action.payload.data.isVerified;
                state.hasProfile = action.payload.data.hasProfile;
            })
            .addCase(getVerificationStatus.rejected, (state, action) => {
                state.loading = false;
                // Don't set error for authentication issues
                if (action.payload !== "User not authenticated or not a farmer") {
                    state.error = action.payload;
                }
            })

            // Request manual verification
            .addCase(requestManualVerification.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(requestManualVerification.fulfilled, (state, action) => {
                state.loading = false;
                state.success = true;
                state.verificationMessage = action.payload.message;
                toast.success(action.payload.message);
            })
            .addCase(requestManualVerification.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload;
                toast.error(action.payload || 'Failed to submit manual verification request');
            });
    }
});

export const {
    clearVerificationError,
    clearVerificationSuccess,
    resetVerificationState
} = verificationSlice.actions;

export default verificationSlice.reducer;
